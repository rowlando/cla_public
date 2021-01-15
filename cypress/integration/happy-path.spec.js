describe('Happy path testing', function() {
  it('Should complete happy path successfully from scope diagnosis to confirmation page', function () {

    cy.visit("https://lga-1543-install-and-integra.staging.checklegalaid.service.gov.uk/start")
    
    cy.savePage('homepage')
    cy.contains('Choose the area you most need help with')
    cy.contains('Debt').click()

    cy.savePage('debt-options')
    cy.contains('Choose the option that best describes your debt problem')
    cy.get(':nth-child(1) > .cla-scope-options-list-item-link').click()

    cy.savePage('scope-outcome')
    cy.contains('Legal aid is available for this type of problem')
    cy.contains('Check if you qualify financially').click()

    const someNumber = 3245;

    // About you form
    cy.savePage('about-you-form')
    cy.contains('.govuk-heading-xl', 'About you')
    cy.setYesNoRadioInput('have_partner', 'No')
    cy.setYesNoRadioInput('on_benefits', 'Yes')
    cy.setYesNoRadioInput('have_children', 'Yes')
    cy.setTextInput('num_children', '4')
    cy.setYesNoRadioInput('have_dependants', 'No')
    cy.setYesNoRadioInput('own_property', 'Yes')
    cy.setYesNoRadioInput('is_employed', 'No')
    cy.setYesNoRadioInput('is_self_employed', 'No')
    cy.setYesNoRadioInput('aged_60_or_over', 'No')
    cy.setYesNoRadioInput('have_savings', 'Yes')
    cy.setYesNoRadioInput('have_valuables', 'No')
    cy.get("#submit-button").click();

    // Which benefits do you receive form
    cy.savePage('which-benefits-do-you-receive-form')
    cy.contains('.govuk-fieldset__heading', 'Which benefits do you receive?')
    cy.setCheckboxInput('benefits-5')
    cy.setCheckboxInput('benefits-6')
    cy.get("#submit-button").click();

    // Your additional benefits form
    cy.savePage('additional-benefits-form')
    cy.contains('.govuk-heading-xl', 'Your additional benefits')
    cy.setCheckboxInput('benefits-6')
    cy.setCheckboxInput('benefits-10')
    cy.setYesNoRadioInput('other_benefits', 'No')
    cy.get("#submit-button").click();

    // Your property form
    cy.savePage('property-form')
    cy.contains('.govuk-heading-xl', 'Your property')
    cy.setYesNoRadioInput('properties-0-is_main_home', 'Yes')
    cy.setYesNoRadioInput('properties-0-other_shareholders', 'Yes')
    cy.setTextInput('properties-0-property_value', someNumber)
    cy.setTextInput('properties-0-mortgage_remaining', someNumber)
    cy.setTextInput('properties-0-mortgage_payments', someNumber)
    cy.setYesNoRadioInput('properties-0-is_rented', 'Yes')
    cy.setTextInput('properties-0-rent_amount-per_interval_value', someNumber)
    cy.setSelectInput('properties-0-rent_amount-interval_period', 'per_week')
    cy.setYesNoRadioInput('properties-0-in_dispute', 'Yes')
    cy.get("#submit-button").click();

    // Your savings form
    cy.savePage('savings-form')
    cy.contains('.govuk-heading-xl', 'Your savings')
    cy.setTextInput('savings', someNumber)
    cy.setTextInput('investments', someNumber)
    cy.get("#submit-button").click();

    // Review your answers page
    cy.savePage('review-page')
    cy.contains('.govuk-heading-xl', 'Review your answers')
    cy.get("#submit-button").click();

    // Contact Civil Legal Advice page
    cy.savePage('contact-CLA')
    cy.contains('.govuk-heading-xl', 'Contact Civil Legal Advice')
    cy.setTextInput('full_name', 'Michael')
    cy.setRadioInput('contact_type-1')
    cy.setTextInput('callback-contact_number', '11111111111')
    cy.setRadioInput('callback-time-specific_day-1')
    cy.get("#submit-button").click();

    // Result confirmation page
    cy.savePage('confirmation-page')
    cy.contains('We will call you back')
    cy.contains('Receive this confirmation by email')
  });
})
