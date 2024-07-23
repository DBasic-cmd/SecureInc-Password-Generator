import secrets
import string
from django.shortcuts  import render

def index(request):
    return render(request, 'generator/index.html')

def generate_password(request):
    length = int(request.GET.get('length', 12))  # Default length is 12 if not specified
    include_uppercase = request.GET.get('uppercase', 'off') == 'on'
    include_lowercase = request.GET.get('lowercase', 'off') == 'on'
    include_digits = request.GET.get('digits', 'on') == 'off'
    include_punctuation = request.GET.get('punctuation', 'off') == 'on'
    exclude_ambiguous = request.GET.get('exclude_ambiguous', 'off') == 'on'
    suggestion = request.GET.get('suggestion', '')

    characters = []
    if include_uppercase:
        characters.extend(string.ascii_uppercase)
    if include_lowercase:
        characters.extend(string.ascii_lowercase)
    if include_digits:
        characters.extend(string.digits)
    if include_punctuation:
        characters.extend(string.punctuation)

    if exclude_ambiguous:
        ambiguous_chars = set('1l0oO')
        characters = [c for c in characters if c not in ambiguous_chars]

    if not characters:
        return render(request, 'generator/password.html', {'message': 'Please select at least one character type.'})

    # Generate the password
    password = list(suggestion)
    while len(password) < length:
        password.append(secrets.choice(characters))

    # Ensure the password is the correct length
    password = ''.join(password[:length])

    # Determine password strength
    if length <= 6:
        strength_message = 'Your password is weak. Consider using a longer password for better security.'
        strength_class = 'text-danger'
    elif 7 <= length <= 9:
        strength_message = 'Your password is of medium strength. A longer password would be stronger.'
        strength_class = 'text-warning'
    else:
        strength_message = 'Your password is strong.'
        strength_class = 'text-success'

    return render(request, 'generator/password.html', {
        'password': password,
        'strength_message': strength_message,
        'strength_class': strength_class
    })