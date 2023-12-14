import os, re, json
# Define the regular expression
regex = r"[^a-zA-Z0-9_-]+"

getAllUsersFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/controllers/getAllUsers.ts"
getUserDataFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/controllers/getUserData.ts"
loginFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/controllers/login.ts"
signUpFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/controllers/signUp.ts"
updateUserFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/controllers/updateUser.ts"

user_files = [getAllUsersFile, getUserDataFile, loginFile, signUpFile, updateUserFile]

validateEmailFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/helpers/validateEmail.ts"
validatePasswordFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/helpers/validatePassword.ts"

helper_files = [validateEmailFile, validatePasswordFile]

dockerIgnoreFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/.dockerignore"
gitIgnoreFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/.gitignore"
dockerFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/Dockerfile"
dockerComposeFile = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/docker-compose.yaml"

root_directory_files = [dockerIgnoreFile, gitIgnoreFile, dockerComposeFile, dockerFile]

dependencies = "@prisma/client bcrypt dotenv express jsonwebtoken"
devDependencies = "@types/bcrypt @types/express @types/jsonwebtoken @types/node nodemon prisma ts-node typescript"

scripts = {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "npx tsc",
    "start": "node dist/index.js",
    "dev": "nodemon src/index.ts"
}

package_json = {
    "name":"",
    "version":"1.0.0",
    "description":"",
    "author":"",
    "license":"ISC",
    "main":"dist/index.js",
    "scripts":scripts,
}

current_dir = os.getcwd()

project_name = input("What is the name of your project: ")

def validate_project_name(name):
    name_includes_space = name != name.strip()
    violates_naming_convention = True if re.search(regex, name) else False
    return name_includes_space or violates_naming_convention


while validate_project_name(project_name):
    project_name = input("Your name should be an alpha-numeric string with no spaces in it: ")

new_dir = f"{current_dir}/{project_name}"

os.mkdir(new_dir)

src_dir = f"{new_dir}/src"
public_dir = f"{new_dir}/public"
prisma_dir = f"{new_dir}/prisma"

os.mkdir(src_dir)

configs_dir = f"{src_dir}/configs"
utils_dir = f"{src_dir}/utils"
middleware_dir = f"{src_dir}/middleware"
users_dir = f"{src_dir}/users"

os.mkdir(configs_dir)
os.mkdir(utils_dir)
os.mkdir(middleware_dir)
os.mkdir(users_dir)
os.mkdir(public_dir)

user_routes = f"{users_dir}/routes"
user_controllers = f"{users_dir}/controllers"
user_helpers = f"{users_dir}/helpers"
user_services = f"{users_dir}/services"

os.mkdir(user_routes)
os.mkdir(user_controllers)
os.mkdir(user_helpers)
os.mkdir(user_services)

package_json["name"] = project_name

with open("test/package.json", "w") as file:
    json.dump(package_json, file)

def curl_file(directory, file):
    command = f"cd {users_dir}/{directory}; wget {file}"
    os.system(command)

cmd = f'cd {project_name}; npm i {dependencies}; npm i {devDependencies} --save-dev'
os.system(cmd)


for file in user_files:
    curl_file("controllers", file)
    
for file in helper_files:
    curl_file("helpers", file)

for file in root_directory_files:
    command = f"cd {project_name}; wget {file}"
    os.system(command)

user_routes_file = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/users/routes/index.ts"
command = f"cd {users_dir}/routes; wget {user_routes_file}"
os.system(command)


auth_middleware_file = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/src/middleware/authenticate.ts"
command = f"cd {middleware_dir}; wget {auth_middleware_file}"
os.system(command)

runner_file = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/run.sh"
command = f"cd {project_name}; wget {runner_file}"
os.system(command)

schema_file = "https://github.com/IamTyrone/Mviyo-Express-Bootcamp/raw/main/prisma/schema.prisma"
os.system(f"cd {project_name};npx prisma init --datasource-provider sqlite")
os.remove(f"{prisma_dir}/schema.prisma")

command = f"cd {prisma_dir}; wget {schema_file}"
os.system(command)

os.system(f"cd {prisma_dir};npx prisma migrate dev --name init")

os.system(f"cd {prisma_dir};prisma generate")


entry_point_code = """// https://blog.logrocket.com/how-to-set-up-node-typescript-express/

// ? Tutorial for initializing Express with TypeScript.

import express from "express";
import dotenv from "dotenv";
import { PrismaClient } from "@prisma/client";
import userRoutes from "./users/routes";

export const prisma = new PrismaClient();

dotenv.config();

const app = express();
const port = process.env.PORT || 9000;

app.use(express.json());

app.use("/api/v1/users", userRoutes);

app.listen(port, () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});"""

f = open(f"{project_name}/src/index.ts", "w")
f.write(entry_point_code)
f.close()

f = open(f"{project_name}/.env", "w")
env_variables = """PORT=9000
JWT_SECRET="ladjs8923newdknq(&87sd)7ds6&$fjsddsfgfhhb@@#$"

# This was inserted by `prisma init`:
# Environment variables declared in this file are automatically made available to Prisma.
# See the documentation for more detail: https://pris.ly/d/prisma-schema#accessing-environment-variables-from-the-schema

# Prisma supports the native connection string format for PostgreSQL, MySQL, SQLite, SQL Server, MongoDB and CockroachDB.
# See the documentation for all the connection string options: https://pris.ly/d/connection-strings

DATABASE_URL="file:./dev.db\""""
f.write(env_variables)
f.close()

os.system(f"chmod +x {project_name}/run.sh")

os.system(f"cd {project_name}; npm run dev")