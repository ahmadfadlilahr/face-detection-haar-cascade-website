# How to Push Your Project to GitHub & Deploy with GitHub Pages

Copyright (c) 2025, [Ahmad Fadlilah](https://github.com/ahmadfadlilah)

Follow these steps to push this project to GitHub and set up GitHub Pages:

## 1. Initialize the Git Repository (if not already done)

```
cd "d:\Projek\New folder\Deteksi Wajah dengan Harr Cascade"
git init
```

## 2. Add All Files to the Repository

```
git add -A
```

## 3. Make the Initial Commit

```
git commit -m "Initial commit with GitHub Pages support"
```

## 4. Create a New Repository on GitHub

- Go to https://github.com/new
- Enter a repository name, e.g., "face-detection-haar-cascade"
- Add a description (optional)
- Choose whether the repository should be public or private
- Do NOT initialize with README, .gitignore, or license (as we already have these files)
- Click "Create repository"

## 5. Connect Your Local Repository to GitHub

After creating your repository on GitHub, you'll see instructions. Run these commands:

```
git remote add origin https://github.com/ahmadfadlilahr/face-detection-haar-cascade.git
git branch -M main
git push -u origin main
```

Replace `ahmadfadlilahr` with your GitHub username.

## 6. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on "Settings"
3. Scroll down to the "GitHub Pages" section
4. Under "Source", select "GitHub Actions" 
5. The GitHub Actions workflow included in this repository will automatically deploy your site

## 7. Customize GitHub Pages Settings

1. Edit the `_config.yml` file:
   - Update the `baseurl` to match your repository name
   - Update the `url` field if you're using a custom domain
   - Update the `author` and other metadata fields

2. Replace all instances of `username` in the project files with your actual GitHub username

## 8. Verify Your GitHub Pages Site

After GitHub Actions has completed the deployment, your site should be available at:
```
https://ahmadfadlilahr.github.io/face-detection-haar-cascade/
```

Replace `ahmadfadlilahr` with your GitHub username.

- Go to https://github.com/ahmadfadlilahr/face-detection-haar-cascade
- You should see all your project files there

## 7. Future Updates

After making changes to your code:

```
git add -A
git commit -m "Description of changes"
git push
```
