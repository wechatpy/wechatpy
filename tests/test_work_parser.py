# -*- coding: utf-8 -*-
import unittest

from wechatpy.work import events, parse_message


class ParseMessageTestCase(unittest.TestCase):
    def test_subscribe_event(self):
        xml = """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[UserID]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[subscribe]]></Event>
            <AgentID>1</AgentID>
        </xml>
        """
        event = parse_message(xml)

        self.assertIsInstance(event, events.SubscribeEvent)
        self.assertEqual(1, event.agent)

    def test_parse_text_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
         <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual("text", msg.type)
        self.assertEqual(1, msg.agent)

    def test_parse_image_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual("image", msg.type)

    def test_parse_voice_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[voice]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <Format><![CDATA[Format]]></Format>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual("voice", msg.type)

    def test_parse_video_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual("video", msg.type)

    def test_parse_location_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[位置信息]]></Label>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual("location", msg.type)

    def test_parse_link_message(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[link]]></MsgType>
        <Title><![CDATA[公众平台官网链接]]></Title>
        <Description><![CDATA[公众平台官网链接]]></Description>
        <Url><![CDATA[url]]></Url>
        <PicUrl><![CDATA[picurl]]></PicUrl>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)
        self.assertEqual("link", msg.type)

    def test_parse_subscribe_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual("event", msg.type)
        self.assertEqual("subscribe", msg.event)

    def test_parse_location_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[LOCATION]]></Event>
        <Latitude>23.137466</Latitude>
        <Longitude>113.352425</Longitude>
        <Precision>119.385040</Precision>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual("event", msg.type)
        self.assertEqual("location", msg.event)
        self.assertEqual(23.137466, msg.latitude)
        self.assertEqual(113.352425, msg.longitude)
        self.assertEqual(119.385040, msg.precision)

    def test_parse_click_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[CLICK]]></Event>
        <EventKey><![CDATA[EVENTKEY]]></EventKey>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual("event", msg.type)
        self.assertEqual("click", msg.event)
        self.assertEqual("EVENTKEY", msg.key)

    def test_parse_view_event(self):
        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[FromUser]]></FromUserName>
        <CreateTime>123456789</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[VIEW]]></Event>
        <EventKey><![CDATA[www.qq.com]]></EventKey>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)

        self.assertEqual("event", msg.type)
        self.assertEqual("view", msg.event)
        self.assertEqual("www.qq.com", msg.url)

    def test_parse_unknown_message(self):
        from wechatpy.messages import UnknownMessage

        xml = """<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[notsure]]></MsgType>
        <MsgId>1234567890123456</MsgId>
        <AgentID>1</AgentID>
        </xml>"""

        msg = parse_message(xml)

        self.assertTrue(isinstance(msg, UnknownMessage))

    def test_parse_modify_calendar(self):
        xml = """
        <xml>
           <ToUserName><![CDATA[toUser]]></ToUserName>
           <FromUserName><![CDATA[fromUser]]></FromUserName>
           <CreateTime>1348831860</CreateTime>
           <MsgType><![CDATA[event]]></MsgType>
           <Event><![CDATA[modify_calendar]]></Event>
           <CalId><![CDATA[wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></CalId>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.ModifyCalendarEvent)
        self.assertEqual("wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA", msg.calendar_id)

    def test_parse_delete_calendar(self):
        xml = """
        <xml>
           <ToUserName><![CDATA[toUser]]></ToUserName>
           <FromUserName><![CDATA[fromUser]]></FromUserName>
           <CreateTime>1348831860</CreateTime>
           <MsgType><![CDATA[event]]></MsgType>
           <Event><![CDATA[delete_calendar]]></Event>
           <CalId><![CDATA[wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></CalId>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.DeleteCalendarEvent)
        self.assertEqual("wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA", msg.calendar_id)

    def test_parse_add_schedule(self):
        xml = """
        <xml>
           <ToUserName><![CDATA[toUser]]></ToUserName>
           <FromUserName><![CDATA[fromUser]]></FromUserName>
           <CreateTime>1348831860</CreateTime>
           <MsgType><![CDATA[event]]></MsgType>
           <Event><![CDATA[add_schedule]]></Event>
           <CalId><![CDATA[wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></CalId>
           <ScheduleId><![CDATA[17c7d2bd9f20d652840f72f59e796AAA]]></ScheduleId>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.AddScheduleEvent)
        self.assertEqual("wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA", msg.calendar_id)
        self.assertEqual("17c7d2bd9f20d652840f72f59e796AAA", msg.schedule_id)

    def test_parse_modify_schedule(self):
        xml = """
        <xml>
           <ToUserName><![CDATA[toUser]]></ToUserName>
           <FromUserName><![CDATA[fromUser]]></FromUserName>
           <CreateTime>1348831860</CreateTime>
           <MsgType><![CDATA[event]]></MsgType>
           <Event><![CDATA[modify_schedule]]></Event>
           <CalId><![CDATA[wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></CalId>
           <ScheduleId><![CDATA[17c7d2bd9f20d652840f72f59e796AAA]]></ScheduleId>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.ModifyScheduleEvent)
        self.assertEqual("wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA", msg.calendar_id)
        self.assertEqual("17c7d2bd9f20d652840f72f59e796AAA", msg.schedule_id)

    def test_parse_delete_schedule(self):
        xml = """
        <xml>
           <ToUserName><![CDATA[toUser]]></ToUserName>
           <FromUserName><![CDATA[fromUser]]></FromUserName>
           <CreateTime>1348831860</CreateTime>
           <MsgType><![CDATA[event]]></MsgType>
           <Event><![CDATA[delete_schedule]]></Event>
           <CalId><![CDATA[wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA]]></CalId>
           <ScheduleId><![CDATA[17c7d2bd9f20d652840f72f59e796AAA]]></ScheduleId>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.DeleteScheduleEvent)
        self.assertEqual("wcjgewCwAAqeJcPI1d8Pwbjt7nttzAAA", msg.calendar_id)
        self.assertEqual("17c7d2bd9f20d652840f72f59e796AAA", msg.schedule_id)

    def test_export(self):
        xml = """
        <xml>
            <ToUserName><![CDATA[wx28dbb14e3720FAKE]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>1425284517</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[batch_job_result]]></Event>
            <BatchJob>
                <JobId><![CDATA[jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4]]></JobId>
                <JobType><![CDATA[export_user]]></JobType>
                <ErrCode>0</ErrCode>
                <ErrMsg><![CDATA[ok]]></ErrMsg>
            </BatchJob>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.ExportEvent)
        self.assertEqual("jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4", msg.job_id)
        self.assertEqual("export_user", msg.job_type)

        xml = """
        <xml>
            <ToUserName><![CDATA[wx28dbb14e3720FAKE]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>1425284517</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[batch_job_result]]></Event>
            <BatchJob>
                <JobId><![CDATA[jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4]]></JobId>
                <JobType><![CDATA[export_simple_user]]></JobType>
                <ErrCode>0</ErrCode>
                <ErrMsg><![CDATA[ok]]></ErrMsg>
            </BatchJob>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.ExportEvent)
        self.assertEqual("jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4", msg.job_id)
        self.assertEqual("export_simple_user", msg.job_type)

        xml = """
        <xml>
            <ToUserName><![CDATA[wx28dbb14e3720FAKE]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>1425284517</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[batch_job_result]]></Event>
            <BatchJob>
                <JobId><![CDATA[jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4]]></JobId>
                <JobType><![CDATA[export_department]]></JobType>
                <ErrCode>0</ErrCode>
                <ErrMsg><![CDATA[ok]]></ErrMsg>
            </BatchJob>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.ExportEvent)
        self.assertEqual("jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4", msg.job_id)
        self.assertEqual("export_department", msg.job_type)

        xml = """
        <xml>
            <ToUserName><![CDATA[wx28dbb14e3720FAKE]]></ToUserName>
            <FromUserName><![CDATA[FromUser]]></FromUserName>
            <CreateTime>1425284517</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[batch_job_result]]></Event>
            <BatchJob>
                <JobId><![CDATA[jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4]]></JobId>
                <JobType><![CDATA[export_taguser]]></JobType>
                <ErrCode>0</ErrCode>
                <ErrMsg><![CDATA[ok]]></ErrMsg>
            </BatchJob>
        </xml>
        """
        msg = parse_message(xml)

        self.assertIsInstance(msg, events.ExportEvent)
        self.assertEqual("jobid_S0MrnndvRG5fadSlLwiBqiDDbM143UqTmKP3152FZk4", msg.job_id)
        self.assertEqual("export_taguser", msg.job_type)

    def test_meeting(self):
        xml = """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[book_meeting_room]]></Event>
            <MeetingRoomId>1</MeetingRoomId>
            <MeetingId><![CDATA[mtebsada6e027c123cbafAAA]]></MeetingId>
        </xml>
        """
        msg = parse_message(xml)
        self.assertIsInstance(msg, events.BookMeetingRoom)
        self.assertEqual(1, msg.meeting_room_id)
        self.assertEqual("mtebsada6e027c123cbafAAA", msg.meeting_id)

        xml = """
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[event]]></MsgType>
            <Event><![CDATA[cancel_meeting_room]]></Event>
            <MeetingId><![CDATA[mtebsada6e027c123cbafAAA]]></MeetingId>
            <MeetingRoomId>1</MeetingRoomId>
        </xml>
        """
        msg = parse_message(xml)
        self.assertIsInstance(msg, events.CancelMeetingRoom)
        self.assertEqual(1, msg.meeting_room_id)
        self.assertEqual("mtebsada6e027c123cbafAAA", msg.meeting_id)
