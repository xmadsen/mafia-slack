from util.slack_payload_parser import parse_payload


def test_convertDelimitedParamsIntoDict():
    raw_args = 'token=testToken&team_id=testId&team_domain=testDomain&channel_id=testChannel&channel_name=privategroup'
    parsed_args = parse_payload(raw_args)
    assert parsed_args['token'] == 'testToken'
    assert parsed_args['team_id'] == 'testId'
    assert parsed_args['team_domain'] == 'testDomain'
    assert parsed_args['channel_id'] == 'testChannel'
    assert parsed_args['channel_name'] == 'privategroup'
