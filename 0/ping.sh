while true; do ts=$(date +"%Y-%m-%d %H:%M:%S"); read t c <<<$(curl -o /dev/null -s -w "%{time_total} %{http_code}" https://google.com); echo "$ts | code=$c | time=${t}s"; sleep 10; done
