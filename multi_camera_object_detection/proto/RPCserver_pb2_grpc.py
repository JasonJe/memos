# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

# import RPCserver_pb2 as RPCserver__pb2
from proto import RPCserver_pb2 as RPCserver__pb2


class ServerInterfaceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.TestStatus = channel.unary_unary(
        '/RPCserver.ServerInterface/TestStatus',
        request_serializer=RPCserver__pb2.PingRequest.SerializeToString,
        response_deserializer=RPCserver__pb2.PongReply.FromString,
        )
    self.ImageStore = channel.unary_unary(
        '/RPCserver.ServerInterface/ImageStore',
        request_serializer=RPCserver__pb2.UploadRequest.SerializeToString,
        response_deserializer=RPCserver__pb2.ResultReply.FromString,
        )


class ServerInterfaceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def TestStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ImageStore(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServerInterfaceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'TestStatus': grpc.unary_unary_rpc_method_handler(
          servicer.TestStatus,
          request_deserializer=RPCserver__pb2.PingRequest.FromString,
          response_serializer=RPCserver__pb2.PongReply.SerializeToString,
      ),
      'ImageStore': grpc.unary_unary_rpc_method_handler(
          servicer.ImageStore,
          request_deserializer=RPCserver__pb2.UploadRequest.FromString,
          response_serializer=RPCserver__pb2.ResultReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'RPCserver.ServerInterface', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
