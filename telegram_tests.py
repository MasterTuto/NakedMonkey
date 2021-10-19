def set_up_commands(bot):
    commands_deleted = bot.delete_commands()

    set_commands = bot.set_commands(
        [
            ("help", "Mostra ajuda"),
            ("rand", "Questao aleatoria baseada em parametros"),
            ("recommend", "Recomenda questao para usuario"),
            ("gen", "Gera PDF com questões de dificuldade easy(+)/medium/hard(+)" )
        ],
        scope=["all_group_chats", "all_private_chats"]
    )

    got_commands = bot.get_commands(scope=["all_group_chats", "all_private_chats"])

    print( commands_deleted.json() )
    print( list( i.json() for i in set_commands ) )
    print( list( r.json() for r in got_commands ) )