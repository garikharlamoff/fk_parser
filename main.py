from parser_class import Parser, measure_time
import time

@measure_time
def main():
    parser = Parser('https://fk.by/computers?filter_ocfilter=p:2000-3000;35381:1751177993;36019:408713063,686690819,797169178,1664062881,2367812749,3336598319,3478535940&limit=25&page=2')
    try:
        while True:
            time.sleep(5)
            parser.get_links_on_page()
            print(len(parser.links_list))
            time.sleep(5)
            parser.go_to_the_next_page()

    except Exception as e:
        print('закончено')

    parser.get_info()
    print(parser.info_list)
    parser.creating_csv_file()


if __name__ == "__main__":
    main()