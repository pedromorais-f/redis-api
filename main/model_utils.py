import torch
from tqdm import tqdm
from timeit import default_timer as timer

def train(epochs, optimizer, criterion, train_loaded, model, metric):
    train_losses = []
    train_accuracies = []

    start_time = timer()

    for epoch in range(epochs):
        train_loss = 0
        
        model.train()
        for index, (images, labels) in tqdm(enumerate(train_loaded), desc=f"Fitting Epoch {epoch + 1}"):

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(outputs, labels)
            train_loss += loss.item()
            loss.backward()

            optimizer.step()


            metric.update(outputs, labels)


        train_loss = train_loss / (index + 1)
        train_accuracy = metric.compute()

        train_losses.append(train_loss)
        train_accuracies.append(train_accuracy)

        print("Epoch: {}/{}  ".format(epoch + 1, epochs),
                "Training loss: {:.4f}  ".format(train_loss),
                "Train accuracy: {:.4f}  \n".format(train_accuracy)
        )

        metric.reset()

    end_time = timer()
    print(f"Time for training: {((end_time - start_time) / 60):.2f} minutes")

    return train_losses, train_accuracies

def eval(model, test_loaded, metric, criterion):
    test_loss = 0

    with torch.no_grad():
        for index, (images, labels) in tqdm(enumerate(test_loaded), desc="Getting accuracy"):

            outputs = model(images)

            loss = criterion(outputs, labels)
            test_loss += loss.item()

            metric.update(outputs, labels)


        test_accuracy = metric.compute()
        test_loss = test_loss / (index + 1)

    print(
        "Test set: Average loss: {:.4f}, Accuracy:{}/{}, {:.4f}\n".format(
            test_loss, int(test_accuracy * 10000), len(test_loaded.dataset), test_accuracy
        )
    )

    return test_loss, test_accuracy