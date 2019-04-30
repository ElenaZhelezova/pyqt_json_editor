# JSON editor #
Скрипт создает или открывает для редактирования .json файл определенной структуры.  

<br>
<br>

#### структура файла:
 
>  {
    'version': ver_#,
       'places': [{'template': 'template_name', 'id': '',
            'setup': {'filial': '', 'reg': '', 'system_host': '',
                  'mas': {'db': {'host': '', 'password': '', 'service_pass': ''}},
                  'easops': {'db': {'host': '', 'password': '', 'service_pass': ''}}
            },
            'win': [{'id': id, 'template': template}]
            }]
        }

