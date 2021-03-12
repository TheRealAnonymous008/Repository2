#ifndef TRUENODE_H
#define TRUENODE_H

#include <AbstractNode.h>


class TRUENode : public AbstractNode
{
    public:
        TRUENode();
        virtual ~TRUENode();
        TRUENode(const TRUENode& other);
        TRUENode& operator=(const TRUENode& other);

    private:
        void Process() override;
};

#endif // TRUENODE_H
