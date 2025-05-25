# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     ROLE_ADMIN         = 'admin'
#     ROLE_PROFESSOR     = 'professor'
#     ROLE_ALUNO         = 'aluno'
#     ROLE_COORDENADOR   = 'coordenador'
#     ROLE_REVISOR       = 'revisor'
#     ROLE_CONVIDADO     = 'convidado'

#     ROLE_CHOICES = [
#         (ROLE_ADMIN,       'Administrador'),
#         (ROLE_PROFESSOR,   'Professor'),
#         (ROLE_ALUNO,       'Aluno'),
#         (ROLE_COORDENADOR, 'Coordenador'),
#         (ROLE_REVISOR,     'Revisor Externo'),
#         (ROLE_CONVIDADO,   'Convidado'),
#     ]

#     role = models.CharField(
#         'Tipo de usuário',
#         max_length=20,
#         choices=ROLE_CHOICES,
#         default=ROLE_CONVIDADO,
#     )

#     def is_admin(self):
#         return self.role == self.ROLE_ADMIN

#     def is_professor(self):
#         return self.role == self.ROLE_PROFESSOR

#     def is_aluno(self):
#         return self.role == self.ROLE_ALUNO

#     def is_coordenador(self):
#         return self.role == self.ROLE_COORDENADOR

#     def is_revisor(self):
#         return self.role == self.ROLE_REVISOR

#     def is_convidado(self):
#         return self.role == self.ROLE_CONVIDADO

#     def has_role(self, *roles):
#         """
#         Retorna True se o usuário tiver qualquer um dos roles passados.
#         """
#         return self.role in roles
