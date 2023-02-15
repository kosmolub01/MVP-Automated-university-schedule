const express = require("express");
const url = require("url");
const execSync = require("child_process").execSync;
const cookieParser = require("cookie-parser");
const app = express();
const port = 3000;

const browser_driver = "path_to_browser_driver"
const py = "path_to_python"
const schedule_screenshot = "path_to_save_schedule_screenshot"

app.use(cookieParser());

// Starting page - if client has a cookie, use it and direct to schedule page.
// If there is no cookie, let the client enter the group name and direct to schedule page
app.get("/", function (req, res) {

  var cookie = req.cookies.group;

  if (cookie === undefined) {
    // Serve the default page with text input
    console.log("Cookie undefined. Serving the starting page");
    res.sendFile("./public/index.html")
  } else {
    // Use cookie
    console.log("Client has a cookie. Waiting for .py script, then serving schedule page");
    const output = execSync(py + " schedule_screenshot.py \"" + cookie + 
    "\" \"" + schedule_screenshot + "\" " + browser_driver);
    res.sendFile("./public/schedule_page.html");
  }
});

// User entered the group name - modify cookie
app.get("/view_schedule", function (req, res) {

  query = url.parse(req.url,true).query;

  // Remove '"'
  let sanitized_group = query.group.replaceAll('"', '');  

  res.cookie("group", sanitized_group, {httpOnly: true});
  console.log("Creating / modifying cookie. Waiting for .py script, then serving schedule page");

  const output = execSync(py + " schedule_screenshot.py \"" + sanitized_group + 
  "\" \"" + schedule_screenshot + "\" " + browser_driver);
  res.sendFile("./public/schedule_page.html");
});

// User wants to change the group
app.get("/change_group", function (req, res) {
  res.sendFile("./public/index.html")
});

app.use(express.static("public"));

app.listen(port, function () {
  console.log(`App listening on port ${port}`);
});
