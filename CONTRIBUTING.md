# Contributing

Pour contribuer à ce projet, merci de suivre les conventions ci-dessous afin de garder un historique clair et cohérent.

---

## 1. Branches

Nous utilisons le **Trunk-Based Development** :  
- `main` est la branche principale, toujours stable.  
- Les autres branches sont **temporaires** et mergées rapidement dans `main`.  

### Convention de nommage
Format :  

| Type    | Usage                      | Exemple |
|---------|----------------------------|---------|
| feat    | Nouvelle fonctionnalité    | feat/login |
| fix     | Correction de bug          | fix/login-error |
| hotfix  | Bug critique en production | hotfix/security |
| chore   | Maintenance / tâches diverses | chore/update-deps |
| docs    | Documentation              | docs/readme |
| refactor| Refactorisation du code    | refactor/auth-service |
| test    | Ajout de tests             | test/login-service |

**Règles :**
- Lettres minuscules  
- Tirets `-` pour séparer les mots  
- Pas d’espaces ni caractères spéciaux  
- Supprimer la branche après merge  

---

## 2. Commits

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/) :

Format :  

| Type    | Usage                      | Exemple |
|---------|----------------------------|---------|
| feat    | Nouvelle fonctionnalité    | feat: add login page |
| fix     | Correction de bug          | fix: correct login redirect |
| docs    | Documentation              | docs: update API usage |
| refactor| Refactorisation            | refactor: simplify auth logic |
| test    | Ajout de tests             | test: add unit test for login |
| chore   | Maintenance / tâches diverses | chore: update dependencies |

**Conseils :**
- Commits courts et ciblés  
- Chaque commit correspond à **une modification logique**  

---

## 3. Versioning / Tags

Nous utilisons [Semantic Versioning (SemVer)](https://semver.org/) :

| Version | Usage |
|---------|-------|
| 0.0.0   | Premier commit initial |
| 0.x.x   | Développement, bug fixes, features |
| 1.0.0   | Première version stable |
| MAJOR.MINOR.PATCH | MAJOR = breaking change, MINOR = nouvelle feature compatible, PATCH = bug fix |

### Tag annoté
```bash
git tag -a 0.0.1 -m "Bug fix login"
git push origin --tags