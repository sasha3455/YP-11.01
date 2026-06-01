from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('djS0rrow', '0002_brand_customer_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='size',
            field=models.CharField(
                default='36',
                max_length=10,
                validators=[
                    django.core.validators.RegexValidator(
                        message='Размер должен быть XS, S, M, L, XL, XXL или числом из 2-3 цифр.',
                        regex='^(XS|S|M|L|XL|XXL|[0-9]{2,3})$'
                    )
                ],
                verbose_name='Размер',
            ),
        ),
    ]
