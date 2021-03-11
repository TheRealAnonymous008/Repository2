#ifndef ORNODE_H
#define ORNODE_H

#include <AbstractNode.h>


class ORNode : public AbstractNode
{
    public:
        ORNode();
        virtual ~ORNode();
        ORNode(const ORNode& other);
        ORNode& operator=(const ORNode& other);

    private:
        void Process() override;
};

#endif // ORNODE_H
