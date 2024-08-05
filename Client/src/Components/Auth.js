import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const Register = () => {
    const { register } = useContext(AuthContext);

    const initialValues = {
        username: '',
        email: '',
        password: '',
    };

    const validationSchema = Yup.object({
        username: Yup.string().required('Username is required'),
        email: Yup.string().email('Invalid email format').required('Email is required'),
        password: Yup.string().required('Password is required'),
    });

    const onSubmit = (values, { setSubmitting }) => {
        register(values.username, values.email, values.password);
        setSubmitting(false);
    };

    return (
        <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={onSubmit}
        >
            {({ isSubmitting }) => (
                <Form>
                    <h2>Register</h2>
                    <div>
                        <Field type="text" name="username" placeholder="Username" />
                        <ErrorMessage name="username" component="div" />
                    </div>
                    <div>
                        <Field type="email" name="email" placeholder="Email" />
                        <ErrorMessage name="email" component="div" />
                    </div>
                    <div>
                        <Field type="password" name="password" placeholder="Password" />
                        <ErrorMessage name="password" component="div" />
                    </div>
                    <button type="submit" disabled={isSubmitting}>Register</button>
                </Form>
            )}
        </Formik>
    );
};

const Login = () => {
    const { login } = useContext(AuthContext);

    const initialValues = {
        email: '',
        password: '',
    };

    const validationSchema = Yup.object({
        email: Yup.string().email('Invalid email format').required('Email is required'),
        password: Yup.string().required('Password is required'),
    });

    const onSubmit = (values, { setSubmitting }) => {
        login(values.email, values.password);
        setSubmitting(false);
    };

    return (
        <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={onSubmit}
        >
            {({ isSubmitting }) => (
                <Form>
                    <h2>Login</h2>
                    <div>
                        <Field type="email" name="email" placeholder="Email" />
                        <ErrorMessage name="email" component="div" />
                    </div>
                    <div>
                        <Field type="password" name="password" placeholder="Password" />
                        <ErrorMessage name="password" component="div" />
                    </div>
                    <button type="submit" disabled={isSubmitting}>Login</button>
                </Form>
            )}
        </Formik>
    );
};

export { Register, Login };
