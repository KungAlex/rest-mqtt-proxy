from flask_restful import fields

subscription_fields = {
    'kind': fields.String,
    'uuid': fields.String,
    'subregex': fields.String,
    'description': fields.String,
    'labels': fields.Raw,
    'event_handlers': fields.Raw,
    'uri': fields.Url('api_subscription_details', absolute=True)
}


topic_mapping_fields = {
    'kind': fields.String,
    'topic': fields.String,
    'uuid': fields.String,
    'sub_uuid': fields.String,
    'last_value': fields.String,
    'last_update': fields.String,
    'details': fields.Url('api_topic_details', absolute=True),
    'uri': fields.Url('api_topic_value', absolute=True)

}
