from flask import jsonify, request

from models.SitesBorrow import SitesBorrow
from . import api_v1


@api_v1.route('/site_borrow', methods=['GET'])
def get_site_bookings():
    return jsonify({"message": "Get all site bookings"})


@api_v1.route('/site_borrow/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    return jsonify({"message": f"Cancel booking {booking_id}"}), 204


@api_v1.route('/site_borrow/available', methods=['GET'])
def get_available_sites():
    return jsonify({"message": "Get available sites"})


# 添加一条待审核的场地借用申请条目
@api_v1.route('/site_borrow', methods=['POST'])
def siteborrow_apply():
    data = request.get_json()
    new_apply = SitesBorrow(apply_id=data.get('apply_id'), \
                            name=data.get('name'), student_id=data.get('student_id'), phonenum=data.get('phonenum'), \
                            email=data.get('email'), purpose=data.get('purpose'), mentor_name=data.get('mentor_name'), \
                            mentor_phone_num=data.get('mentor_phone_num'), picture=data.get('picture'),
                            start_time=data.get('start_time'), \
                            end_time=data.get('end_time'))
    SitesBorrow.session.add(new_apply)
    SitesBorrow.session.commit()
    return jsonify({"code": 200,
                    "status": "success",
                    "message": "申请提交成功",
                    "data": {"apply_id": data.get('apply_id')}
                    }
                   )


# 更改场地借用申请的状态键
@api_v1.route('/site_borrow', methods=['post'])
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
            "updated_at": "2024-02-13T15:30:00Z"  # TODO 要改成当前时间戳
        }
    }
    )


# 基管部审核⻚面拉取信息。
@api_v1.route('/site_borrow/<string:apply_id>', methods=['GET'])
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
