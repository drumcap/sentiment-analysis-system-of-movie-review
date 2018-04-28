# -*- coding: utf-8 -*-

import json
from bothub_client.bot import BaseBot
from bothub_client.messages import Message
from bothub_client.decorators import command
from .movies import BoxOffice
from .movies import LotteCinema


class Bot(BaseBot):

    def on_default(self, event, context):
        '''dispatcher에 의해 처리되지 않은, 다른 메세지들을 처리할 기본 handler'''

        # 메세지 문자열을 가져온다
        content = event.get('content')
        location = event.get('location')

        # 메세지가 없다면
        if not content:
            # 봇이 들어있는 단체방에 누군가 들어온다면 new_joined에 값이 참으로 들어온다.
            # 만약 event에 new_joined 값이 있으며, 그 값이 참이면,
            if 'new_joined' in event and event['new_joined']:
                # 메세지를 보낸다
                self.send_chatroom_welcome_message(event)
            # 함수를 종료한다
            return

        if location:
            self.send_nearest_theaters(location['latitude'], location['longitude'], event)
            return

        # 구문에 대한 이해를 DialogFlow로 전송
        recognized = self.recognize(event, context)
        if recognized:
            return

        self.send_error_message(event)

    def recognize(self, event, context):
        response = self.nlu('apiai').ask(event=event)
        action = response.action

        message = Message(event)

        if action.intent == 'input.unknown':
            return False

        # if not action.completed:
        #     message.set_text(response.next_message)
        #     self.send_message(message)
        #     return True

        if action.intent == 'hit-movies':
            message.set_text(response.next_message)
            self.send_message(message)
            self.send_box_office(event, context, [])
            return True

        if action.intent == 'movie-sentiment':
            message.set_text(response.next_message)
            self.send_message(message)
            params = action.parameters
            # self.send_order(event, context, (params['menu'], params['quantity']))
            message2 = Message(event).set_text(params['movie-name'])
            self.send_message(message2)
            return True

        message.set_text(response.next_message)
        self.send_message(message)
        return True

    @command('boxoffice')
    def send_box_office(self, event, context, args):
        data = self.get_project_data()
        api_key = data.get('box_office_api_key')
        box_office = BoxOffice(api_key)
        movies = box_office.simplify(box_office.get_movies())
        rank_message = '\n'.join(['{}. {}'.format(m['rank'], m['name']) for m in movies])
        response = '요즘 볼만한 영화들의 순위입니다\n{}'.format(rank_message)

        message = Message(event).set_text(response)\
                                .add_quick_reply('영화순위', '/boxoffice')\
                                .add_quick_reply('근처 상영관 찾기', '/find')
        self.send_message(message)

    @command('find')
    def send_search_theater_message(self, event, context, args):
        message = Message(event).set_text('현재 계신 위치를 알려주세요')\
                                .add_location_request('위치 전송하기')
        self.send_message(message)

    def send_nearest_theaters(self, latitude, longitude, event):
        c = LotteCinema()
        theaters = c.get_theater_list()
        nearest_theaters = c.filter_nearest_theater(theaters, latitude, longitude)

        message = Message(event).set_text('가장 가까운 상영관들입니다.\n' + \
                                          '상영 시간표를 확인하세요:')

        for theater in nearest_theaters:
            data = '/schedule {} {}'.format(theater['TheaterID'], theater['TheaterName'])
            message.add_postback_button(theater['TheaterName'], data)

        message.add_quick_reply('영화순위')
        self.send_message(message)

    @command('schedule')
    def send_theater_schedule(self, event, context, args):
        theater_id = args[0]
        theater_name = ' '.join(args[1:])

        c = LotteCinema()
        movie_id_to_info = c.get_movie_list(theater_id)

        text = '{}의 상영시간표입니다.\n\n'.format(theater_name)

        movie_schedules = []
        for info in movie_id_to_info.values():
            movie_schedules.append('* {}\n  {}'.format(info['Name'], ' '.join([schedule['StartTime'] for schedule in info['Schedules']])))

        message = Message(event).set_text(text + '\n'.join(movie_schedules))\
                                .add_quick_reply('영화순위', '/boxoffice')\
                                .add_quick_reply('근처 상영관 찾기', '/find')
        self.send_message(message)

    @command('start')
    def send_welcome_message(self, event, context, args):
        message = Message(event).set_text('반가워요.\n\n'\
                                          '저는 요즘 볼만한 영화들을 알려드리고, '\
                                          '현재 계신 곳에서 가까운 영화관들의 상영시간표를 알려드려요.\n\n'
                                          "'영화순위'나 '근처 상영관 찾기'를 입력해보세요.")\
                                .add_quick_reply('영화순위', '/boxoffice')\
                                .add_quick_reply('근처 상영관 찾기', '/find')
        self.send_message(message)

    def send_error_message(self, event):
        message = Message(event).set_text('잘 모르겠네요.\n\n'\
                                          '저는 요즘 볼만한 영화들을 알려드리고, '\
                                          '현재 계신 곳에서 가까운 영화관들의 상영시간표를 알려드려요.\n\n'
                                          "'영화순위'나 '근처 상영관 찾기'를 입력해보세요.")\
                                .add_quick_reply('영화순위', '/boxoffice')\
                                .add_quick_reply('근처 상영관 찾기', '/find')
        self.send_message(message)