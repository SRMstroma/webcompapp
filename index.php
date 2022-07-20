<html>
<head>
<title>ツイート定期検索&保存β</title>
<head>
<body>
<form action = "/test.py" method = "post">
<div><label for ="word">
検索ワード(リツイートは自動的に除かれます)<br>
<input type = "text" id = "word" name = "word">
</label>
</div>
<div><label for = "sheet">
保存先(webcomp-srm@srmmarzwebcomp.iam.gserviceaccount.comに共有が必要です)<br>
<input type = "text" id = "sheet" name = "sheet">
</label></div>
<div>
<input type = "submit" value = "更新">
</form>