#include <gtest/gtest.h>

void setup(void){
    // setup for tests
}

void test_example(void){
    TEST_ASSERT_EQUAL(1, 1);
    TEST_ASSERT_EQUAL(2, 2);
}



void loop(void){
    RUN_TEST(test_example);
}