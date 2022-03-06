# Получаем значение SEO для нашего видео с YouTube.

## Библиотеки для работы
* pytube
- Windows:
  python3 -m pip install pytube
- Debian:
  pip3 install pytube
  
## Получение SEO

  from get_seo import GetSeo
  
  
  seo = GetSeo('https://www.youtube.com/watch?v=2i2khp_npdE') <br>
  print(seo.seo) #93.0704742904924<br>

## Доступные данные о видео:<br>
  seo.tags # Список тегов видео<br>
  seo.tags_position # Список тегов с позицией в поиске<br>
  seo.video_description # Описание видео<br>
  seo.video_title # Заголовок видео<br>
  seo.video_id # ID видео<br>
  
  
