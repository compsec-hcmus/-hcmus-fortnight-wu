<?php
  class Logger {
    public $command;
    // More attributes to come

    function __construct(string $message = "") {
      $this->command = 'echo ("' . $message . '");';
    }

    function __destruct() {
      // No need to explicitly call, how clever am I.
      eval($this->command);
    }
  }

  function get_flag() {
    echo $_ENV["flag"];
  }
?>

<html>
  <head>
    <title>Object oriented programming - supreme</title>
    <link rel="stylesheet" href="static/style.css">
  </head>

  <body>
    <h1>Message echo-er</h1>
    <h3>Repeats the messages you want to send to yourself.</h3>
    <div class="container">
      <div id="form" class="content">
        <h2>Send your messages here:</h2>
        <input id="message" type="text" placeholder="your message">
        <button onclick="handleSend()">
          Send!
        </button>
      </div>
      <div class="message">
        <h2>Your message</h2>
        <?php
          if (isset($_GET["msg"])) {
            // TODO: create a new class for message ;)
            $msg = unserialize(base64_decode($_GET["msg"]));
            
            try {
              $logger = new Logger("You sent the message: " . $msg["content"]);
            } catch (Exception $ex) {
              // Automatically handle problem of invalid object
              // How clever am I
              $logger = new Logger("Oops, something happened");
            }
          }
        ?>
      </div>
    </div>

    <script>
      function handleSend() {
        const elem = document.getElementById("message");
        const message = elem.value;
        serialized_obj = `a:1:{s:7:"content";s:${message.length}:"${message}";}`;

        console.log(serialized_obj, btoa(serialized_obj));

        document.location = document.location.origin + "?msg=" + btoa(serialized_obj);
      }
    </script>
  </body>
</html>