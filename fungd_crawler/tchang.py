# # -*- coding: utf-8 -*-

import sys
import os
import pathlib
import argparse
import requests
from bs4 import BeautifulSoup

from article_class import Article

sys.setrecursionlimit(10000)


global_title_list = []
global_article_list = []


def get_item_list(page=1):
    page_url1 = f'https://tgd.kr/funzinnu/page/{page}'
    soup1 = BeautifulSoup(requests.get(url=page_url1).text, 'html.parser')
    return soup1.select('div.item')

if __name__ == "__main__":
    # 인자 파싱 
    parser = argparse.ArgumentParser(description="Fungd crawler")
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

    # 조건 : 댓글이 늘어났거나 새 글임

    line_length = 80
    line = '〓' * line_length  # 구분선이 너무 길다 싶으면 줄이세요
    line1 = '▼' * line_length
    line2 = '▲' * line_length

    print(f'{line}\n목록 점검 중\n')
    with open(dir1, 'r') as file1:
        num = int(file1.readline())

        article_list = \
            (lambda l: [Article(e) for e in l if Article.is_item_valid(e)])(get_item_list(1))
        article_new = \
            (lambda l: [e.visit_link() for e in l if e.id > num])(article_list)
        article_new.sort(key=(lambda e: e.id))

        print(line1)
        if article_new:
            num = article_new[-1].id
            for ele in article_new:
                expr = f'{ele.vote=},\t{ele.reply_count=}\n' \
                    f'{ele.writer=}, {ele.title=}\n\n' \
                    f'{ele.content}'
                print(expr)
                print(line)
        else:
            print("새로운 글이 없습니다.")

    print(f"가장 최근 글 id: {num}")
    print(line2)

    with open(dir1, 'w') as file1:
        file1.write(str(num))
    
    # 정상종료
    sys.exit(0)
