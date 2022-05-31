from tflite_runtime.interpreter import Interpreter
from PIL import Image
import numpy as np

def classify_image(interpreter, image, top_k=1):
  tensor_index = interpreter.get_input_details()[0]['index']
  #input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor = np.expand_dims(np.array(image, dtype=np.float32),axis=0)
  interpreter.set_tensor(tensor_index,input_tensor)
  print(np.expand_dims(np.array(image),axis=0).shape)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  #output = np.squeeze(interpreter.get_tensor(output_details['index']))

  #scale, zero_point = output_details['quantization']
  #output = scale * (output - zero_point)

  #ordered = np.argpartition(-output, top_k)
  rand_var = interpreter.get_tensor(output_details["index"])
  print(rand_var)
  #return [(i, output[i]) for i in ordered[:top_k]][0]
  return rand_var
def load_labels(path): # Read the labels from the text file as a Python list.
  with open(path, 'r') as f:
    return [line.strip() for i, line in enumerate(f.readlines())]


model_path = "/home/rr/Documents/warehouse/finalModel3.tflite"
label_path = "/home/rr/Documents/warehouse/labels.txt"
interpreter = Interpreter(model_path)
interpreter.allocate_tensors()
_,h,w,_ = interpreter.get_input_details()[0]["shape"]
print(h)
print(w)
rat = Image.open("/home/rr/Documents/warehouse/fire4.jpg").convert("RGB").resize((w,h))
tensor_index = interpreter.get_input_details()
print(tensor_index)
label_id = classify_image(interpreter,rat)
print(np.argmax(label_id[0]))
labels = load_labels(label_path)
class_label = labels[np.argmax(label_id[0])]
print(class_label)


