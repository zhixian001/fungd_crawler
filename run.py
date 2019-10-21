# -*- coding: utf-8 -*-

import sys
import argparse
import pathlib

from fungd_crawler import tchang

if __name__ == "__main__":
    # 인자 파싱 
    parser = argparse.ArgumentParser(prog="fungd_crawler", description="Fungd crawler")
    parser.add_argument('outputfile', metavar='FILEPATH', type=str, help="크롤링에 사용할 파일의 경로")
    parser.add_argument("-N", "--new-output-file", type=int, help="옵션 활성화 시 output파일을 주어진 정수 값으로 새로 만듭니다.", default=10, required=False)
    parser.add_argument("-f", "--force" , action='store_true', help="이 옵션을 사용하면 output 파일이 이미 존재하더라도 새 파일을 만들어 덮어씁니다. -N 옵션이 없으면 아무런 효과가 없습니다.", required=False)

    args = parser.parse_args()

    # 경로 지정
    dir1 = pathlib.Path(args.outputfile)

    # 파일 존재 여부 확인
    if (dir1.is_file()):
        # 파일 존재
        if (args.new_output_file and args.force):
            # 새 파일 덮어쓰기
            with dir1.open(mode='w') as f:
                f.write(str(args.new_output_file))
        else:
            # 새 파일을 만들지 않음
            pass
    else:
        # 파일 없음
        if (args.new_output_file):
            # 새 파일 만들기
            with dir1.open(mode='w') as f:
                f.write(str(args.new_output_file))

        else:
            # 파일이 없는데 새 파일 만들기 옵션이 없는 경우
            print("파일이 없습니다. -N 옵션을 사용하세요.")
            sys.exit(1)
    
    # 크롤러 호출
    exit_code = tchang.crawler_main(dir1)

    # 종료
    sys.exit(exit_code)
