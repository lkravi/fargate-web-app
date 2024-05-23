python3 -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt -t .

mkdir package
cp -r myenv/lib/python3.8/site-packages/* package/
cp lambda_function.py package/
cd package
zip -r ../lambda.zip .
cd ..

deactivate
