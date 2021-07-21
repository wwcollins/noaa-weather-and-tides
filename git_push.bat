echo "Repo:  https://github.com/wwcollins/noaa-weather.git"
git remote add origin https://github.com/wwcollins/noaa-weather.git
echo "Repo:  https://github.com/wwcollins/noaa-weather.git"
git pull
git add . -f
git commit -m "committing recent changes" 
git branch -M main
git push -u origin main
echo "Script Completed..."