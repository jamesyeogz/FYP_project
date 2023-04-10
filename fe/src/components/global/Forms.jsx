import React from "react";

const Forms = ({ initialState }) => {
  const [form, setForm] = React.useState({ ...initialState });
  const submitForm = (e) => {
    e.preventDefault();
    for (var key in initialState) {
      if (form.key === "") {
        // Stop the form from passing through
        console.log(key);
        return { missing: key, res: false };
      }
    }
    return { missing: "", res: true };
  };
  const handleForm = (e) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: value,
    });
    console.log(form);
  };
  const clearForm = () => {
    setForm({ ...initialState });
  };
  return {
    form,
    submitForm,
    handleForm,
    clearForm,
    setForm,
  };
};

export default Forms;
