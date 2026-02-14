#!/usr/bin/python
import os
import re
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            port=dict(type='int', required=True),
            config_path=dict(type='str', default='/etc/nginx/nginx.conf')
        ),
        supports_check_mode=True
    )

    port = module.params['port']
    path = module.params['config_path']

    if not (1 <= port <= 65535):
        module.fail_json(msg=f"Недопустимый номер порта: {port}")

    if not os.path.exists(path):
        module.fail_json(msg=f"Файл конфигурации не найден: {path}")

    try:
        with open(path, encoding='utf-8') as f:
            text = f.read()

        # Самый надёжный способ замены
        new_text = re.sub(
            r"(listen\s+)\d+;",
            lambda m: m.group(1) + str(port) + ";",
            text,
            count=1
        )

        changed = (text != new_text)

        if changed and not module.check_mode:
            # делаем бэкап
            backup_path = path + f".bak.{port}"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(text)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_text)

        module.exit_json(
            changed=changed,
            msg="Порт уже был таким" if not changed else f"Порт изменён на {port}",
            backup_created=changed and not module.check_mode
        )

    except Exception as e:
        module.fail_json(msg=f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()