# ベースのshell
# ubuntu: つまりubuntuベースのDockerfileのみを取得する
grep "ubuntu:" -rl sources | xargs -J% cp % ubuntu