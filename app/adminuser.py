#-*- coding: UTF-8 -*- 
from flask import Blueprint
from flask import request,jsonify,json
from models import *
import models 
from hashmd5 import *
import string

adminuser_route = Blueprint('adminuser_route', __name__)

@adminuser_route.route("/getallactivity",methods=['POST'])
def signup():
	try:
		token = request.json['token']
		page = request.json.get('page','1')
		x=string.atoi(str(page))
		u=getuserinformation(token)
		if u!=None and u.username == 'administrator':
			pagetemp = Activity.query.order_by(models.Activity.top.desc()).order_by(models.Activity.timestamp.desc()).paginate(x, per_page=10, error_out=False)
			actlist = pagetemp.items
			result = []
			state = 'successful'
			reason = ''
			for act in actlist:
				title = act.title if act.title!=None else ''  
				time = act.time if act.time!=None else ''
				location=act.location if act.location!=None else ''
				number=act.number if act.number!=None else ''
				remark = act.remark if act.remark != None else ''
				advertise = act.advertise if act.advertise != None else ''
				detail = act.detail if act.detail != None else ''
				whetherimage = act.whetherimage if act.whetherimage != None else ''
				signnumber = act.users.count()
				signnumber = str(signnumber)
				author = act.author.name if act.authorid != None else ''
				authorid = act.authorid if act.authorid != None else ''
				school = act.author.school if act.authorid != None else ''
				gender = act.author.gender if act.authorid != None else ''
				if act.passflag == '1':
					passflag = '通过'
				elif act.passflag == '2':
					passflag = '未通过'
				else:
					passflag = '审核中'
				#获取活动的海报
				poster = activityimageAttach.query.filter_by(activityid = act.id,imageid = 0).first()
				if poster != None:
					image = "http://218.244.147.240:80/activity/activityimages/"+ str(act.id)+'-'+'0'
				else:
					image = ""
				output = {'id':act.id,'author':author,'authorid':authorid,'school':school,'gender':gender,'title':title,'time':time,'location':location,'number':number,'signnumber':signnumber,'remark':remark,'detail':detail,'advertise':advertise,'whetherimage':whetherimage,"imageurl":image,'state':passflag}
				result.append(output)
		else:
			state = 'fail'
			reason = '用户不存在'
			result = []
	except Exception, e:
		print e
		state = 'fail'
		reason = '异常'
		result = []

	response = jsonify({'result':result,
						'state':state,
						'reason':reason})
	return response

@adminuser_route.route("/setpassactivity",methods=['POST'])
def setpassactivity():
	try:
		token = request.json['token']
		activitylist = request.json['activitylist']
		u = getuserinformation(token)	
		if u != None and u.username == 'administrator':	
			state = 'successful'
			reason = ''
			for activityid in activitylist:
				activity = getactivitybyid(activityid)
				if activity != None:
					activity.passflag = '1'
					activity.add()
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response

@adminuser_route.route("/setnopassactivity",methods=['POST'])
def setnopassactivity():
	try:
		token = request.json['token']
		activitylist = request.json['activitylist']
		u = getuserinformation(token)	
		if u != None and u.username == 'administrator':	
			state = 'successful'
			reason = ''
			for activityid in activitylist:
				activity = getactivitybyid(activityid)
				if activity != None:
					activity.passflag = '2'
					activity.add()
		else:
			state = 'fail'
			reason = '非法用户'
			result = ''
	except Exception, e:
		print e
		result = ''
		state = 'fail'
		reason = 'exception'
	response = jsonify({'state':state,                                                                                                                                                                                  
						'reason':reason})
	return response
