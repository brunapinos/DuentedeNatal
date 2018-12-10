import asyncio
from functools import reduce
from telepot import glance, message_identifier
import telepot.aio
import telepot.aio.helper
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.aio.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)


votes = dict()

class DuenteBot(telepot.aio.helper.ChatHandler):
    def _init_(self, *args, **kwargs):
        super(VoteCounter, self).__init__(*args, **kwargs)

        global votes
        if self.id in votes:
            self._ballot_box, self._keyboard_msg_ident, self._expired_event, self._member_count = votes[self.id]
            self._editor = telepot.aio.helper.Editor(self.bot, self._keyboard_msg_ident) if self._keyboard_msg_ident else None
        else:
            self._ballot_box = None
            self._keyboard_msg_ident = None
            self._editor = None
            self._expired_event = None
            self._member_count = None
        
        # Catch _join_expired event
        self.router.routing_table['_expired'] = self.on__join_expired

    def _count_votes(self):
        yes = reduce(lambda a,b: a+(1 if b=='yes' else 0), self._ballot_box.values(), 0)
        # no = reduce(lambda a,b: a+(1 if b=='no' else 0), self._ballot_box.values(), 0)
        return yes


    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = glance(msg)

        if content_type != 'text':
            print('Not a text message.')
            return

        if msg['text'] == '/start':
            print(telepot.flavor(msg))
            await self._init_ballot()
        elif msg['text'] == '/close': 
# # Generate an expiry event 30 seconds later
            # self._expired_event = self.scheduler.event_later(5, ('x', {'seconds': 5}))
            self._expired_event = self.scheduler.event_now(('chat', {'seconds': 10}))
            # # self._close_ballot()

# Init join of sorting

    async def _init_ballot(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                       InlineKeyboardButton(text='Participar', callback_data='yes'),
                   ]])
        sent = await self.sender.sendMessage("Vamos participar do Amigo Oculto!!", reply_markup=keyboard)

        self._member_count = await self.administrator.getChatMembersCount() - 1  # exclude myself, the bot

        self._ballot_box = {}
        self._keyboard_msg_ident = message_identifier(sent)
        self._editor = telepot.aio.helper.Editor(self.bot, self._keyboard_msg_ident)
        
        

    async def _close_ballot(self):

        # self._expired_event = self.scheduler.event_now(('_join_expired',{'seconds': 1}))
        print('tesbdfhjsbhbfsjbhdfsbfhbshdbfsbhdjhfsbjdhf')
        self.scheduler.cancel(self._expired_event)

        await self._editor.editMessageReplyMarkup(reply_markup=None)

        self._ballot_box = None
        self._keyboard_msg_ident = None
        self._editor = None


    async def on_callback_query(self, msg):
        query_id, from_id, query_data = glance(msg, flavor='callback_query')

        if from_id in self._ballot_box:
            await self.bot.answerCallbackQuery(query_id, text='Você já está participando %s' % self._ballot_box[from_id])
        else:
            await self.bot.answerCallbackQuery(query_id, text='Ok')
            self._ballot_box[from_id] = query_data

        # Announce results if everyone has voted.
        if len(self._ballot_box) >= self._member_count:
            result = self._count_votes()
            await self._close_ballot()
            await self.sender.sendMessage('Everyone has voted:\nYes: %d\nNo: %d\nSilent: %d' % result)

    async def on__join_expired(self, event):
        result = self._count_votes()
        await self._close_ballot()
        await self.sender.sendMessage('Time is up:\nYes: %d' % result)

    def on_close(self, ex):
        global votes
        if self._ballot_box is None:
            try:
                del votes[self.id]
            except KeyError:
                pass
        else:
            votes[self.id] = (self._ballot_box, self._keyboard_msg_ident, self._expired_event, self._member_count)

        from pprint import pprint
        print('%d closing ...' % self.id)
        pprint(votes)






TOKEN = '678582209:AAGdYnxxV3SkRKzWm8BBR8ur4ozAcozzxQo'

bot = telepot.aio.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['group']), create_open, DuenteBot, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()