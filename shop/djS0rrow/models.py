from django.db import models
from django.core.validators import RegexValidator

MAX_LENNGHT = 255
SIZE_VALIDATOR = RegexValidator(
    regex=r'^(XS|S|M|L|XL|XXL|[0-9]{2,3})$',
    message='Размер должен быть XS, S, M, L, XL, XXL или числом из 2-3 цифр.',
)


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENNGHT, verbose_name='Наименование категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENNGHT, verbose_name='Наименование коллекции')
    description = models.TextField(null=True, blank=True, verbose_name='Описание коллекции')
    season = models.CharField(max_length=100, null=True, blank=True, verbose_name='Сезон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


class Brand(models.Model):
    name = models.CharField(max_length=MAX_LENNGHT, verbose_name='Наименование бренда')
    description = models.TextField(null=True, blank=True, verbose_name='Описание бренда')
    country = models.CharField(max_length=MAX_LENNGHT, null=True, blank=True, verbose_name='Страна')
    logo = models.ImageField(
        upload_to='brands/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Логотип',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Clothes(models.Model):
    name = models.CharField(max_length=MAX_LENNGHT, verbose_name='Наименование одежды')
    description = models.TextField(null=True, blank=True, verbose_name='Описание одежды')
    price = models.FloatField(verbose_name='Цена')
    size = models.CharField(max_length=10, default='36', verbose_name='Размер', validators=[SIZE_VALIDATOR])
    color = models.CharField(max_length=MAX_LENNGHT, verbose_name='Цвет')
    photo = models.ImageField(
        upload_to='image/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    is_exists = models.BooleanField(default=True, verbose_name='Доступность')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    collection = models.ManyToManyField(Collection, verbose_name='Коллекция', blank=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд',
    )

    def __str__(self):
        return f'{self.name} — {self.price} руб.'

    class Meta:
        verbose_name = 'Позиция одежды'
        verbose_name_plural = 'Позиции одежды'


class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='Покупатель')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )
    total_amount = models.FloatField(default=0, verbose_name='Сумма заказа')

    def __str__(self):
        return f'Заказ №{self.pk} — {self.customer}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    clothes = models.ForeignKey(Clothes, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price_at_order = models.FloatField(verbose_name='Цена на момент заказа')

    def __str__(self):
        return f'{self.clothes.name} × {self.quantity}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'


class Review(models.Model):
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    text = models.TextField(null=True, blank=True, verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    def __str__(self):
        return f'Отзыв на {self.clothes.name} — {self.rating}/5'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
