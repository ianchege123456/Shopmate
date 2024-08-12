import React from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { submitSupportRequest } from '../../api';

const validationSchema = Yup.object({
  message: Yup.string().required('Message is required'),
});

const SupportForm = () => {
  const handleSubmit = async (values, { setSubmitting, setErrors }) => {
    try {
      await submitSupportRequest(values);
      alert('Your request has been submitted');
    } catch (error) {
      setErrors({ general: 'Failed to submit request' });
    }
    setSubmitting(false);
  };

  return (
    <Formik
      initialValues={{ message: '' }}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      <Form>
        <div>
          <label htmlFor="message">Message</label>
          <Field as="textarea" id="message" name="message" />
          <ErrorMessage name="message" component="div" />
        </div>
        <button type="submit">Submit</button>
        <ErrorMessage name="general" component="div" />
      </Form>
    </Formik>
  );
};

export default SupportForm;
