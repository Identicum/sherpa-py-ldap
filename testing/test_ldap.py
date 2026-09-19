#!/usr/bin/env python3

import os
import sys

from sherpa.utils.basics import Logger

sys.path.insert(0, './sherpa/ldap/')
from ldap_lib import LDAP


def main():
	logger = Logger(os.path.basename(__file__), "DEBUG", "/tmp/sherpa-py-ldap.log")
	run(logger)
	logger.info("{} finished.".format(os.path.basename(__file__)))


def create_ldap_objects(ldap: LDAP, base_dn: str, users_base_dn: str, groups_base_dn: str):
	ldap.create_ad_ou(base_dn=base_dn, name="sherpa_users", ignore_if_exists=True)
	ldap.create_ad_ou(base_dn=base_dn, name="sherpa_groups", ignore_if_exists=True)
	group_members = []
	for i in range(2):
		ldap.create_ad_user(base_dn=users_base_dn, username=f"testuser{i}", password="testPassword.2025", upn=f"testuser{i}@idsherpa.com", given_name="Test", last_name="User1", ignore_if_exists=True)
		group_members.append((f"cn=testuser{i},{users_base_dn}").encode())
	for i in range(2):
		ldap.create_ad_group(base_dn=groups_base_dn, name=f"testgroup{i}", description=f"Test group {i}", members=group_members, ignore_if_exists=True)


def run(logger):
	logger.info("{} starting.".format(os.path.basename(__file__)))

	ip_address = "samba"
	base_dn = "dc=idsherpa,dc=com"
	admin_dn = "cn=administrator,cn=users,{}".format(base_dn)
	admin_password = "Sherpa.2025"
	ldap = LDAP(ip_address=ip_address, user_dn=admin_dn, user_password=admin_password, logger=logger)
	users_base_dn = "ou=sherpa_users,{}".format(base_dn)
	groups_base_dn = "ou=sherpa_groups,{}".format(base_dn)

	create_ldap_objects(ldap=ldap, base_dn=base_dn, users_base_dn=users_base_dn, groups_base_dn=groups_base_dn)

	for object in ldap.get_objects(base_dn=users_base_dn, filter="(objectclass=user)", page_size=20):
		cvs_row = ldap.get_attributes_csv(object, attr_list=["cn","sn","givenName","employeeID","title", "employeeType", "memberOf", "department"], multivalue_separator="##")
		logger.info("CSV row: {}", cvs_row)

	ldap.get_object(object_dn="ou=sherpa_groups,dc=idsherpa,dc=com")

	ldap.get_object(object_dn="cn=testgroup1,ou=sherpa_groups,dc=idsherpa,dc=com")


if __name__ == "__main__":
	sys.exit(main())

