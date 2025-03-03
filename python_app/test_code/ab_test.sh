#!/bin/bash
# generating web requests to the builders-frontend
# 하나의 URL에 두개의 URI path를 대상으로 test traffic을 Apache Benchmark tool로 생성

# 테스트할 기본 URL 설정
TEST_URL="<PUT_DOWN_YOUR_TEST_URL>" # Test URL 입력

# 총 요청 수와 동시 연결수 설정
TOTAL_REQUESTS=15000
CONCURRENT_REQUESTS=150

# 반복 횟수
REPEAT_COUNT=30

# 랜덤 요청 생성 함수
gen_request_random() {
    # /cat 또는 /dog 중 하나를 랜덤으로 선택
    if (( RANDOM % 2 == 0 )); then
        URI="/cat"
    else
        URI="/dog"
    fi

    echo "Running ab test with url: $TEST_URL$URI"

    # Apache Bench 실행
    ab -n $TOTAL_REQUESTS -c $CONCURRENT_REQUESTS "$TEST_URL$URI"

}

for (( i=1; i<=REPEAT_COUNT; i++))
do
        gen_request_random

done

echo "Test completed."
