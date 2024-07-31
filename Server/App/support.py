from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import SupportTicket, User

bp = Blueprint('support', __name__, url_prefix='/api/support')

# Route to submit a new support ticket
@bp.route('/tickets', methods=['POST'])
@jwt_required()
def submit_ticket():
    data = request.get_json()
    if not data or 'subject' not in data or 'message' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    user_id = get_jwt_identity()['id']
    ticket = SupportTicket(
        user_id=user_id,
        subject=data['subject'],
        message=data['message'],
        status='Open'
    )
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify({'message': 'Support ticket submitted successfully', 'ticket_id': ticket.id}), 201

# Route to get all support tickets for the current user
@bp.route('/tickets', methods=['GET'])
@jwt_required()
def get_tickets():
    user_id = get_jwt_identity()['id']
    tickets = SupportTicket.query.filter_by(user_id=user_id).all()
    
    ticket_list = [
        {
            'id': ticket.id,
            'subject': ticket.subject,
            'message': ticket.message,
            'status': ticket.status,
            'created_at': ticket.created_at
        } for ticket in tickets
    ]
    return jsonify(ticket_list), 200

# Route to get details of a specific support ticket
@bp.route('/tickets/<int:id>', methods=['GET'])
@jwt_required()
def get_ticket(id):
    user_id = get_jwt_identity()['id']
    ticket = SupportTicket.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    ticket_data = {
        'id': ticket.id,
        'subject': ticket.subject,
        'message': ticket.message,
        'status': ticket.status,
        'created_at': ticket.created_at
    }
    return jsonify(ticket_data), 200

# Route to update the status of a support ticket (admin only)
@bp.route('/tickets/<int:id>', methods=['PUT'])
@jwt_required()
def update_ticket_status(id):
    # Assuming there's a mechanism to check if the user is an admin
    if not get_jwt_identity().get('is_admin'):
        return jsonify({'message': 'Permission denied'}), 403
    
    data = request.get_json()
    ticket = SupportTicket.query.get_or_404(id)
    ticket.status = data.get('status', ticket.status)
    db.session.commit()
    
    return jsonify({'message': 'Support ticket status updated successfully'}), 200
