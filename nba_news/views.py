import logging.config
from memory_profiler import profile
from config import NbaHotNewsConfig
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NBANews, NBANewsDetail
from .serializers import NBANewsSerializer
from .handler.page_parse import SearchLastPage, MutableMainbar, DetailPageInfo


log = logging.getLogger(__name__)

url = NbaHotNewsConfig.NBA_HOT_NEWS_FIREST_PAGE

class NBANewsView(APIView):
    def get(self, request, *args, **kwargs):

        page_number = int(request.query_params.get(
            'page_number', 1))  # 照著頁碼給參數 沒給就第一頁

        page_size = 10
        offset = (page_number - 1) * page_size

        nba_news = NBANews.objects.all()[offset:offset+page_size].values()

        return Response({'message': 'success', "payload": nba_news}, status=200)


class NBANewsDetailView(APIView):
    def get(self, request, *args, **kwargs):

        nba_news_id = request.query_params.get('nba_news_id')
        return_data = {}

        if nba_news_id == None:
            return Response({'message': 'missing required field', "payload": []}, status=400)

        try:
            nba_news_detail = NBANewsDetail.objects.get(
                nba_news_id=nba_news_id)

            return_data['title'] = nba_news_detail.detail_title
            return_data['author'] = nba_news_detail.author
            return_data['paragraph'] = nba_news_detail.paragraph

            return Response({'message': 'success', "payload": return_data}, status=200)

        except:
            return Response({'message': 'Data not found', "payload": []}, status=400)


class CronJobView(APIView):   # 排程API
    @profile
    def get(self, request, *args, **kwargs):

        first_slash_from_bottom = url.rfind('/')
        url_without_page = url[:first_slash_from_bottom + 1]

        last_page = SearchLastPage(url)

        if last_page == 0:
            return Response({'message': 'last page number is weird', "payload": []}, status=200)

        insert_data = []
        filter_data = []
        detail_page_data = []

        for i in range(1, (last_page+1)):   # 爬資料
            mutable_url = url_without_page + str(i)
            a, b = MutableMainbar(mutable_url)

            insert_data += a
            filter_data += b

        nba_news = NBANews.objects.filter(detail_url__in=filter_data)  # 內容頁的URL作為判斷新聞是否有更新
        detail_url_amount = len(filter_data)

        if detail_url_amount == len(nba_news):
            return Response({'message': 'Nothing to update', "payload": []}, status=200)

        for detail_url in filter_data:   # 爬內容頁, 先爬再刪舊資料不然爬太久會影響GET, 內存消耗可能比較大一點但可以換來GET資料穩定
            data = DetailPageInfo(detail_url)
            detail_page_data += data

        nba_all_obj = NBANews.objects.all()
        nba_all_detail_obj = NBANewsDetail.objects.all()
        nba_all_obj.delete()
        nba_all_detail_obj.delete()

        serializer = NBANewsSerializer(data=insert_data, many=True)

        if serializer.is_valid():
            instances = [NBANews(**item) for item in serializer.validated_data]
            NBANews.objects.bulk_create(instances)
            insert_infos = NBANews.objects.all()

            for i in range(len(insert_infos)):
                detail_page_data[i]["nba_news_id"] = insert_infos[i].id
                NBANewsDetail.objects.create(**detail_page_data[i])

        logging.info('Cron job done')
        # Websocket

        return Response({'message': 'success', "payload": [last_page]}, status=200)
