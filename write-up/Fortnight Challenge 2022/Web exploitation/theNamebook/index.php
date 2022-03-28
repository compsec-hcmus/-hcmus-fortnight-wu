<?php
  $db = new SQLite3('db.db'); // TODO: Upgrade to proper database later

  function sanitize($table) {
    $pattern = '/' . implode(['union', 'select', 'from', 'where', 'group', 'by', 'and'], '|') . '/i';
    return preg_replace($pattern, '', $table);
  }

  if (isset($_POST['table']) && isset($_POST['id'])) {
    $id = $_POST['id'];
    $table = sanitize($_POST['table']);
    $stmt = $db->prepare('SELECT id, username FROM ' . $table . ' WHERE id=:id;');
    $stmt->bindParam(':id', $id, SQLITE3_INTEGER);
    $result = $stmt->execute();
  }
?>

<html>
  <head>
    <title>The Namebook</title>
    <link rel="stylesheet" href="static/style.css">
  </head>
  <body>
    <h3>Welcome to</h3>
    <h1>the<b>NAMEBOOK</b></h1>
    <div class="container">
      <p>An encyclopedia about everyone in the uni, still in progress</p>
      <form method="post">
        <input name="table" id="table" type="hidden" value="user">
        <input name="id" id="id" type="text" placeholder="id of the user">
        <button type="submit">
          Send!
        </button>
      </form>
      <table>
        <thead>
          <th>
            ID
          </th>
          <th>
            Username
          </th>
        </thead>
        <tbody>
          <?php
            while ($result && $array = $result->fetchArray(SQLITE3_ASSOC)) {
              echo '<tr><td>' . $array['id'] . '</td><td>' . $array['username'] . '</td></tr>';
            }
          ?>
        </tbody>
      </table>
    </div>
  </body>
</html>