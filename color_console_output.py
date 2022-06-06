def color_console_output()
  header = '\033[95m'
  blue = '\033[94m'
  cyan = '\033[96m'
  green = '\033[92m'
  warning = '\033[93m'
  fail = '\033[91m'
  reset = '\033[0m'
  bold = '\033[1m'
  underline = '\033[4m'
  
  message = print("Message with " + blue + "blue" + reset + " color!")
  return message
  

if __name__ == '__main__':
  color_console_output()
