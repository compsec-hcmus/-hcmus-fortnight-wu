<?php
  $username = "admin";
  $password = "240610708"; // My magical lucky number

  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST["username"]) && isset($_POST["password"])) {
      if ($_POST["username"] == $username) {
        // Shout out to md5 for being sooooo secure UwU
        if (md5($_POST["password"]) == md5($password)) {
          if ($_POST["password"] != $password) {
            die("Well done, here is your flag " . $_ENV["flag"]);
          }
          die("Muahahaha, damedame desu");
        }
      }
      die("... the credential is right there :)");
    }
    else {
      die("Are u sure u typed all the fields?");
    }
  }
?>


<html>
  <head>
    <title>Impossible login</title>
    <link rel="stylesheet" href="static/style.css">
  </head>

  <body>
    <h3>Welcome to the</h3>
    <h1>impossible login panel</h1>

    <form method="post">
      <label>Username</label>
      <div data-validate="Enter username">
        <input class="input" type="text" name="username">
      </div>

      <label>Password</label>
      <div data-validate="Enter password">
        <input class="input" type="password" name="password">
      </div>

      <div>
        <button>
          Login
        </button>
      </div>
    </form>
  </body>
</html>