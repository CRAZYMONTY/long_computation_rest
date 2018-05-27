import setuptools as st

st.setup(
    name="test_gunicorn", version="1.0.0", packages=st.find_packages(exclude=("tests"))
)
