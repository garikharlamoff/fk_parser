from parser_class import Parser
import time


def main():
    print('zap')
    parser = Parser('https://mile.by/catalog/799-elektroobogrevateli/obogrevatel-elektricheskiy/')
    print('вып')
    # parser.accept_cookie()
    try:
        while True:
            time.sleep(1)
            parser.get_links_on_page()
            print(len(parser.links_list))
            time.sleep(1)
            parser.go_to_the_next_page()

    except Exception as e:
        print(e)

    parser.get_info()
    print(parser.info_list)
    parser.creating_csv_file()


if __name__ == "__main__":
    main()

