def form_result(info):
    poster = info['poster']

    caption = f"Фильм: {info['name']}\n" \
              f"Рейтинг: {info['rating']}\n" \
              f"Год: {info['year']}\n\n" \
              f"{info['description']}"

    return poster, caption


def form_single_card(info):
    print(info)
    poster = info['poster']['url']

    caption = f"Фильм: {info['name']}\n" \
              f"Рейтинг: {info['rating']['kp']}\n" \
              f"Год: {info['year']}\n\n" \
              f"{info['description']}"
    # markup = tt.InlineKeyboardMarkup()
    #
    # if info['externalId']['kpHD'] is not None:
    #     btn_my_site = tt.InlineKeyboardButton(
    #         text='Смотреть онлайн',
    #         url=f"https://hd.kinopoisk.ru/film/{info['externalId']['kpHD']}")
    #     markup.add(btn_my_site)