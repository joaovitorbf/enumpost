<!--Simple vulnerable to enumeration login form-->

<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Enumerate Me</title>
    </head>
    <body style="font-family: helvetica, sans-serif;">
        <center>
            <h1>Enumerate Me</h1>
            <form action="/index.php" method="post">
            Username:<br>
            <input type="text" name="username">
            <br>
            Password:<br>
            <input type="password" name="password">
            <br><br>
            <input type="submit" name="submit" value="Enter">
            </form>
            <?php
                if (isset($_POST['submit'])) {
                    $username = $_POST['username'];
                    $password = $_POST['password'];
                    if ($username == 'john' or $username == 'mary') {
                        if ($password == 'password123') {
                            echo('Logged in');
                        } else {
                            echo('Wrong password');
                        }
                    } else {
                        echo('Username does not exist');
                    }
                }
            ?>
        </center>
    </body>
</html>