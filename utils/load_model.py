import tensorflow
from tensorflow.core.protobuf.rewriter_config_pb2 import RewriterConfig
import numpy as np

tf = tensorflow.compat.v1

class SSDFaceMask(object):
    def __init__(self, model_dir):
        # config = tf.ConfigProto()
        # custom_op = config.graph_options.rewrite_options.custom_optimizers.add()
        # custom_op.name = "NpuOptimizer"
        # custom_op.parameter_map["use_off_line"].b = True
        # custom_op.parameter_map["precision_mode"].s = tf.compat.as_bytes("force_fp16")
        # custom_op.parameter_map["graph_run_mode"].i = 0
        # config.graph_options.rewrite_options.remapping = RewriterConfig.OFF
        # config.graph_options.rewrite_options.memory_optimization = RewriterConfig.OFF

        self.input_tensor_name = 'serving_default_input:0'
        self.output_tensor_name = 'StatefulPartitionedCall:0'

        self.graph = tf.Graph()
        self.sess = tf.InteractiveSession(graph = self.graph)
        self.output_tensor = self.load_model(model_dir)

    def load_model(self, model_dir):
        '''carrega um saved_model salvo em 'model_dir'
        e retorna o tensor'''
        _ = tf.saved_model.load(self.sess, ['serve'], model_dir)
        output_tensor = self.graph.get_tensor_by_name(self.output_tensor_name)
        return output_tensor
    
    def inference(self, frame, score_threshold=0.5):
        #frame = tf.image.resize(frame.astype('uint8'), (320,320))
        frame = np.expand_dims(frame, 0)
        r = self.sess.run(self.output_tensor, feed_dict={self.input_tensor_name: frame}) # shape = (1,10,6) [ymin, xmin, ymax, xmax, class, score]
        # scores = r[..., 5]
        # classes = r[..., 4]
        # boxes = r[..., :4]
        # filter = np.where(scores > score_threshold)
        return r#boxes[filter], classes[filter], scores[filter]
    