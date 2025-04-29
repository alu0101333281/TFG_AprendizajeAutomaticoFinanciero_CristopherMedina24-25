App de backtesting para analisis financiero


COMMANDS:

ejecutar el servidor con express
node backend/server.js
accedemos a la web
http://localhost:5000
Activar el entorno virtual de python
venv\Scripts\activate
Ejecuta la API de backtesting de python
python -m uvicorn main:app --reload
accedemos a la web
http://localhost:8000

Para ejecutar el backend y frontend de manera concurrente ejecutamos desde la raiz:
npm run dev

El warning que sale es debido a que vite recomienda usar module pero estamos usando commonjs que en este caso es mejor
para evitar errores y mantener tu código más compatible con librerías actuales. Es lo más estable en entornos Node.js sin configuración adicional.

Se podria solucionar creando un package.json dentro del front con el type en module.