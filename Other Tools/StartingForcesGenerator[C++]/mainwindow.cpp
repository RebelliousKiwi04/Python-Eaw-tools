#include "mainwindow.h"
#include <QVBoxLayout>
#include <QLabel>
#include <QHBoxLayout>
#include <QComboBox>
#include <QTableWidget>
#include <QSpinBox>
#include <QPushButton>
#include <Qt>
#include <QHeaderView>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("Starting Forces File Generator");
    setMinimumWidth(500);
    QWidget *mainWidget = new QWidget;
    setCentralWidget(mainWidget);
    QVBoxLayout *mainLayout = new QVBoxLayout;
    mainWidget->setLayout(mainLayout);


    QVBoxLayout *existingForcesLayout = new QVBoxLayout;
    QLabel *existingForcesLabel = new QLabel;
    existingForcesLabel->setText("All Starting Forces");
    existingForcesLabel->setAlignment(Qt::AlignCenter);
    existingForcesLayout->addWidget(existingForcesLabel);

    QTableWidget *existingForces = new QTableWidget;
    existingForces->setColumnCount(3);
    QStringList horzHeaders;
    horzHeaders << "Planet" << "Owner" << "Tech";
    existingForces->setHorizontalHeaderLabels(horzHeaders);
    existingForces->horizontalHeader()->setSectionResizeMode(0,QHeaderView::Stretch);
    existingForces->verticalHeader()->setVisible(false);
    existingForcesLayout->addWidget(existingForces);

    mainLayout->addLayout(existingForcesLayout);



    QHBoxLayout *planetLayout = new QHBoxLayout;
    QLabel *label2 = new QLabel;
    label2->setText("Planet:");
    label2->setFixedWidth(45);
    QComboBox *planetName = new QComboBox;
    planetLayout->addWidget(label2);
    planetLayout->addWidget(planetName);

    mainLayout->addLayout(planetLayout);

    QHBoxLayout *ownerLayout = new QHBoxLayout;
    QLabel *ownerLabel = new QLabel;
    ownerLabel->setText("Planet Owner:");
    ownerLabel->setFixedWidth(75);
    QComboBox *planetOwner = new QComboBox;
    ownerLayout->addWidget(ownerLabel);
    ownerLayout->addWidget(planetOwner);


    mainLayout->addLayout(ownerLayout);

    QHBoxLayout *unitLayout = new QHBoxLayout;
    QLabel *unitLabel = new QLabel;
    unitLabel->setText("Unit:");
    unitLabel->setFixedWidth(35);
    QComboBox *allUnits = new QComboBox;

    unitLayout->addWidget(unitLabel);
    unitLayout->addWidget(allUnits);

    mainLayout->addLayout(unitLayout);

    QHBoxLayout *quantityLayout = new QHBoxLayout;

    QLabel *quantityLabel = new QLabel;
    quantityLabel->setText("Quantity:");
    quantityLabel->setFixedWidth(55);
    QSpinBox *quantity = new QSpinBox;

    quantityLayout->addWidget(quantityLabel);
    quantityLayout->addWidget(quantity);

    mainLayout->addLayout(quantityLayout);



    QHBoxLayout *techLayout = new QHBoxLayout;
    QLabel *techLabel = new QLabel;
    techLabel->setText("Tech:");
    techLabel->setFixedWidth(35);
    QSpinBox *tech = new QSpinBox;
    techLayout->addWidget(techLabel);
    techLayout->addWidget(tech);

    mainLayout->addLayout(techLayout);

    QPushButton *addUnit = new QPushButton;
    addUnit->setText("Add Unit");

    mainLayout->addWidget(addUnit);


    QHBoxLayout *buttonLayout = new QHBoxLayout;

    QPushButton *saveButton = new QPushButton;
    QPushButton *cancelButton = new QPushButton;

    saveButton->setText("Generate File");
    cancelButton->setText("Cancel");
    buttonLayout->addWidget(saveButton);
    buttonLayout->addWidget(cancelButton);

    mainLayout->addLayout(buttonLayout);
}

MainWindow::~MainWindow()
{
}
