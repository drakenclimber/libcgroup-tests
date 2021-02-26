/**
 * libcgroup googletest for v2_weight_to_v1()
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

class CgroupV2WeightToV1: public ::testing::Test {
};

TEST_F(CgroupV2WeightToV1, NullWeightVal)
{
	struct cgroup_controller cgc = {0};
	char *weight_val = NULL;
	int ret;

	ret = v2_weight_to_v1(&cgc, weight_val);
	ASSERT_EQ(ret, ECGINVAL);
	ASSERT_EQ(weight_val, nullptr);
	ASSERT_EQ(cgc.index, 0);
}

TEST_F(CgroupV2WeightToV1, EmptyWeightVal)
{
	struct cgroup_controller cgc = {0};
	char *weight_val = "";
	int ret;

	ret = v2_weight_to_v1(&cgc, weight_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.shares");
	ASSERT_STREQ(cgc.values[0]->value, "");
}

TEST_F(CgroupV2WeightToV1, ValidWeight1)
{
	struct cgroup_controller cgc = {0};
	char *weight_val = "100";
	int ret;

	ret = v2_weight_to_v1(&cgc, weight_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.shares");
	ASSERT_STREQ(cgc.values[0]->value, "1024\n");
}

TEST_F(CgroupV2WeightToV1, ValidWeight2)
{
	struct cgroup_controller cgc = {0};
	char *weight_val = "400";
	int ret;

	ret = v2_weight_to_v1(&cgc, weight_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.shares");
	ASSERT_STREQ(cgc.values[0]->value, "4096\n");
}

TEST_F(CgroupV2WeightToV1, ValidWeight3)
{
	struct cgroup_controller cgc = {0};
	char *weight_val = "50";
	int ret;

	ret = v2_weight_to_v1(&cgc, weight_val);
	ASSERT_EQ(ret, 0);
	ASSERT_EQ(cgc.index, 1);
	ASSERT_STREQ(cgc.values[0]->name, "cpu.shares");
	ASSERT_STREQ(cgc.values[0]->value, "512\n");
}
