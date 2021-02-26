/**
 * libcgroup googletest for v1_shares_to_v2()
 *
 * Copyright (c) 2021 Oracle and/or its affiliates.
 * Author: Tom Hromatka <tom.hromatka@oracle.com>
 */

/*
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of version 2.1 of the GNU Lesser General Public License as
 * published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
 * for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, see <http://www.gnu.org/licenses>.
 */

#include "gtest/gtest.h"
#include "abstraction-common.h"
#include "libcgroup-internal.h"

class CgroupV1SharesToV2: public ::testing::Test {
};

TEST_F(CgroupV1SharesToV2, NullSharesVal)
{
	struct cgroup_controller cgc = {0};
	char *shares_val = NULL;
	int ret;

	ret = v1_shares_to_v2(&cgc, shares_val);
	ASSERT_EQ(ret, ECGINVAL);
	ASSERT_EQ(shares_val, nullptr);
	ASSERT_EQ(cgc.index, 0);
}

TEST_F(CgroupV1SharesToV2, EmptySharesVal)
{
	struct cgroup_controller cgc = {0};
	char *shares_val = "";
	int ret;

	ret = v1_shares_to_v2(&cgc, shares_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.weight");
	ASSERT_STREQ(cgc.values[0]->value, "");
}

TEST_F(CgroupV1SharesToV2, ValidShares1)
{
	struct cgroup_controller cgc = {0};
	char *shares_val = "1024";
	int ret;

	ret = v1_shares_to_v2(&cgc, shares_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.weight");
	ASSERT_STREQ(cgc.values[0]->value, "100\n");
}

TEST_F(CgroupV1SharesToV2, ValidShares2)
{
	struct cgroup_controller cgc = {0};
	char *shares_val = "2048";
	int ret;

	ret = v1_shares_to_v2(&cgc, shares_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.weight");
	ASSERT_STREQ(cgc.values[0]->value, "200\n");
}

TEST_F(CgroupV1SharesToV2, ValidShares3)
{
	struct cgroup_controller cgc = {0};
	char *shares_val = "256";
	int ret;

	ret = v1_shares_to_v2(&cgc, shares_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.weight");
	ASSERT_STREQ(cgc.values[0]->value, "25\n");
}
