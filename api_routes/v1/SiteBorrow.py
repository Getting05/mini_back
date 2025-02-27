from flask import jsonify, request
from sqlalchemy import func
from models.SitesBorrow import SitesBorrow, db
from . import api_v1
import iso8601

iso_time_str = "2022-01-01T12:00:00Z"
iso_time = iso8601.parse_date(iso_time_str)
print(iso_time)


# 获取场地借用booking条目
@api_v1.route('/site-borrow', methods=['GET'])
def get_site_bookings():
    items = db.query(SitesBorrow.type.distinct()).all()
    return {
        "code": 200,
        "status": "success",
        "message": "场地借用数据条目获取成功",
        "data": [item[0] for item in items]
    }


# 取消一条场地借用申请
@api_v1.route('/site-borrow/<int:apply_id>', methods=['DELETE'])
def cancel_booking(apply_id):
    booking = SitesBorrow.query.filter_by(id=apply_id).first()
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": f"Cancel booking {apply_id}"}), 204
    else:
        return jsonify({"message": f"Booking {apply_id} not found"}), 404


# 获取所有可借用的场地, 不可用，没有可借用场地表对应其状态，无法单从场地借用申请表中获取可借用场地
@api_v1.route('/site-borrow/available', methods=['GET'])
def get_available_sites():
    data = request.get_json()
    start_time = iso8601.parse_date(data.get('start_time'))
    end_time = iso8601.parse_date(data.get('end_time'))
    available_sites = SitesBorrow.query.filter(
        iso8601.parse_date(SitesBorrow.start_time) >= start_time,
        iso8601.parse_date(SitesBorrow.end_time) <= end_time,
        SitesBorrow.state != 1)
    return jsonify({
        "code": 200,
        "status": "success",
        "message": "Get available sites",
        "data": [site.site_name for site in available_sites]
    })


# 添加一条待审核的场地借用申请条目
@api_v1.route('/site-borrow', methods=['POST'])
def siteborrow_apply():
    data = request.get_json()
    new_apply = SitesBorrow(apply_id=data.get('apply_id'), name=data.get('name'), student_id=data.get('student_id'),
                            phonenum=data.get('phonenum'),
                            email=data.get('email'), purpose=data.get('purpose'), mentor_name=data.get('mentor_name'),
                            mentor_phone_num=data.get('mentor_phone_num'), picture=data.get('picture'),
                            start_time=data.get('start_time'), end_time=data.get('end_time'))
    SitesBorrow.session.add(new_apply)
    SitesBorrow.session.commit()
    return jsonify({"code": 200,
                    "status": "success",
                    "message": "申请提交成功",
                    "data": {"apply_id": data.get('apply_id')}
                    }
                   )


# 更改场地借用申请的状态键
@api_v1.route('/site-borrow', methods=['post'])
def get_site_bookings():
    data = request.get_json()
    apply = SitesBorrow.query.filter_by(apply_id=data.get('apply_id')).first()
    if data.get('state') == 1:
        apply.state = 1
        SitesBorrow.session.commit()
    return jsonify({
        "code": 200,
        "status": "success",
        "message": "状态更新成功",
        "data": {
            "apply_id": data.get('apply_id'),
            "state": 1,
            "updated_at": func.now()
        }
    }
    )


# 基管部审核页面拉取信息。
@api_v1.route('/site-borrow/<string:apply_id>', methods=['GET'])
def pull_booking(apply_id):
    if apply_id:
        apply_data = SitesBorrow.query.filter_by(apply_id=apply_id).first()
        return jsonify({"code": 200, "status": "success", "message": "success", "data": {
            "apply_id": apply_id,
            "name": apply_data.name,
            "student_id": apply_data.student_id,
            "phonenum": apply_data.phonenum,
            "email": apply_data.email,
            "purpose": apply_data.purpose,
            "mentor_name": apply_data.mentor_name,
            "mentor_phone_num": apply_data.mentor_phone_num,
            "picture": apply_data.picture,
            "start_time": apply_data.start_time,
            "end_time": apply_data.end_time,
            "state": apply_data.state,
            "created_at": apply_data.creat_at
        }})
    else:
        return jsonify({"message": "Fail!"})
